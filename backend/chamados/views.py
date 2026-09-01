from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .models import Chamado
from .serializers import ChamadoSerializer

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
            
            # 3. Valida se o status enviado é aceito
            if status_param not in status_permitidos:
                raise ValidationError({
                    "status": f"Status '{status_param}' é inválido. Valores aceitos: {', '.join(status_permitidos)}."
                })
            
            # 4. Aplica o filtro no banco de dados
            queryset = queryset.filter(status=status_param)

        return queryset

class ChamadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer