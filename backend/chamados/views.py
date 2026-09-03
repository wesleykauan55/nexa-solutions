from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Chamado
from .serializers import ChamadoSerializer

##
class ChamadoListCreateView(generics.ListCreateAPIView):
    serializer_class = ChamadoSerializer

    def get_queryset(self):
        # 1. Pega todos os chamados
        queryset = Chamado.objects.all()
        
        # 2. Captura o parâmetro 'status' da URL (?status=ABERTO)
        status_param = self.request.query_params.get('status', None)

        if status_param is not None:
            status_param = status_param.upper()
            status_permitidos = ['ABERTO', 'EM_ANDAMENTO', 'CONCLUIDO']
            
            # 3. Tratamento de parâmetro inválido (Critério de Aceite)
            if status_param not in status_permitidos:
                raise ValidationError({
                    "status": f"Status '{status_param}' é inválido. Escolha entre: ABERTO, EM_ANDAMENTO, CONCLUIDO."
                })
            
            # 4. Aplica o filtro (Critério de Aceite)
            queryset = queryset.filter(status=status_param)

        return queryset

class ChamadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer

class IndicadoresView(APIView):
    def get(self, request):
        total = Chamado.objects.count()
        abertos = Chamado.objects.filter(status='ABERTO').count()
        em_andamento = Chamado.objects.filter(status='EM_ANDAMENTO').count()
        concluidos = Chamado.objects.filter(status='CONCLUIDO').count()

        return Response({
            'total': total,
            'abertos': abertos,
            'em_andamento': em_andamento,
            'concluidos': concluidos
        })