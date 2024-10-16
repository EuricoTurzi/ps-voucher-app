import qrcode
from pathlib import Path
from django.db import models
from motoristas.models import Motorista
from rotas.models import Rota
from django.conf import settings

class Voucher(models.Model):
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE)
    valor_restante = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    codigo = models.CharField(max_length=50, unique=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    status = models.CharField(max_length=50, default='Pendente')
    usado = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.codigo = self._generate_unique_code()
            self.qr_code = self._generate_qr_code(self.codigo)
        if not self.pk:  # Apenas na criação
            self.valor_restante = self.rota.valor_total
        super().save(*args, **kwargs)

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
