from django.db import models

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    peso = models.FloatField()
    altura = models.FloatField()
    genero = models.CharField(max_length=10) 
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100,default="senha")
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    plano_alimentar = models.FileField(upload_to="pdfs/",blank=True, null=True)

    def __str__(self):
        return self.nome

class Nutricionista(models.Model):
    nome = models.CharField(max_length=100,null=False)
    email = models.EmailField(unique=True,null=False)
    senha = models.CharField(max_length=100,null=False,default="senha")
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
    
class Consulta(models.Model):

    data_consulta = models.DateTimeField(null=True,blank=False)

    nutricionista = models.ForeignKey(Nutricionista,on_delete=models.CASCADE)

    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)

    realizada = models.BooleanField(default=False)