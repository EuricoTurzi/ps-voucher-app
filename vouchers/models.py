import qrcode
from pathlib import Path
from django.db import models
from motoristas.models import Motorista
from rotas.models import Rota
from django.conf import settings
from django.contrib.auth.models import User  # Para referenciar o usuário
from datetime import timedelta
from django.utils.timezone import now  # Importar `now` para lidar com datas no timezone do Django


class Voucher(models.Model):
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE)
    valor_restante = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    codigo = models.CharField(max_length=50, unique=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    status = models.CharField(max_length=50, default='Pendente')
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Novo campo
    data_criacao = models.DateTimeField(auto_now_add=True)  # Novo campo
    
    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.codigo = self._generate_unique_code()
            self.qr_code = self._generate_qr_code(self.codigo)
        if not self.pk:  # Apenas na criação
            self.valor_restante = self.rota.valor_total
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.status in ['Pendente', 'Ativo'] and now() > self.data_criacao + timedelta(hours=24)

    def _generate_unique_code(self):
        import uuid
        return str(uuid.uuid4())

    def _generate_qr_code(self, codigo):
        qr_code_dir = Path(settings.MEDIA_ROOT) / 'qrcodes'
        qr_code_dir.mkdir(parents=True, exist_ok=True)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(codigo)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = qr_code_dir / f'{codigo}.png'
        img.save(img_path)
        return f'qrcodes/{codigo}.png'
