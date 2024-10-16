from django.db import models
from vouchers.models import Voucher
from postos.models import Posto

class GastoVoucher(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    posto = models.ForeignKey(Posto, on_delete=models.CASCADE)
    valor_gasto = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Gasto de {self.valor_gasto} no posto {self.posto.nome}'