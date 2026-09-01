from rest_framework import serializers
from .models import Chamado

class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado
        fields = [
            "id",
            "titulo",
            "descricao",
            "status",
            "criado_em",
            "atualizado_em",
        ]

        # Correção da falha: Tornamos o título obrigatório e não permitimos branco
        extra_kwargs = {
            "titulo": {
                "required": True,
                "allow_blank": False,
            },
        }

        read_only_fields = [
            "id",
            "criado_em",
            "atualizado_em",
        ]

    # Validação extra para impedir que o usuário envie apenas espaços "   "
    def validate_titulo(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("O título do chamado não pode estar vazio ou conter apenas espaços.")
        return value