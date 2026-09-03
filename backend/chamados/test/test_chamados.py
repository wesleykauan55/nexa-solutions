from rest_framework import status
from rest_framework.test import APITestCase

from chamados.models import Chamado


class ChamadoTests(APITestCase):

    def test_nao_permite_cadastro_sem_titulo(self):
        dados = {
            "titulo": "",
            "descricao": "Chamado sem título",
            "status": "ABERTO",
        }

        resposta = self.client.post(
            "/api/chamados/",
            dados,
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn("titulo", resposta.data)
        self.assertEqual(Chamado.objects.count(), 0)

    def test_permite_cadastro_valido(self):
        dados = {
            "titulo": "Computador não liga",
            "descricao": "O computador da recepção não está ligando.",
            "status": "ABERTO",
        }

        resposta = self.client.post(
            "/api/chamados/",
            dados,
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(Chamado.objects.count(), 1)
        self.assertEqual(resposta.data["titulo"], "Computador não liga")
        self.assertEqual(resposta.data["status"], "ABERTO")


class ChamadoFiltroTests(APITestCase):

    def setUp(self):
        Chamado.objects.create(
            titulo="Erro no sistema",
            descricao="...",
            status="ABERTO",
        )
        Chamado.objects.create(
            titulo="Ajuste de tela",
            descricao="...",
            status="EM_ANDAMENTO",
        )
        Chamado.objects.create(
            titulo="Atualização DB",
            descricao="...",
            status="CONCLUIDO",
        )

    def test_filtro_por_status_valido(self):
        resposta = self.client.get(
            "/api/chamados/?status=ABERTO"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(resposta.data), 1)
        self.assertEqual(resposta.data[0]["status"], "ABERTO")

    def test_filtro_por_status_invalido(self):
        resposta = self.client.get(
            "/api/chamados/?status=BATATA"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class IndicadoresTests(APITestCase):

    def setUp(self):
        Chamado.objects.create(
            titulo="Incidente 1",
            descricao="...",
            status="ABERTO",
        )
        Chamado.objects.create(
            titulo="Incidente 2",
            descricao="...",
            status="EM_ANDAMENTO",
        )
        Chamado.objects.create(
            titulo="Incidente 3",
            descricao="...",
            status="CONCLUIDO",
        )
        Chamado.objects.create(
            titulo="Incidente 4",
            descricao="...",
            status="CONCLUIDO",
        )

    def test_obter_indicadores(self):
        resposta = self.client.get("/api/indicadores/")

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(resposta.data["total"], 4)
        self.assertEqual(resposta.data["abertos"], 1)
        self.assertEqual(resposta.data["em_andamento"], 1)
        self.assertEqual(resposta.data["concluidos"], 2)