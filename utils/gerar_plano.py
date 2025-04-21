from types import SimpleNamespace
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
import json
def gerar_pdf(plano):
    # Converte JSONField para dict se for string
    dados_json = plano.dados_json
    if isinstance(dados_json, str):
        dados_json = json.loads(dados_json)

    dados_json_obj = json.loads(json.dumps(dados_json), object_hook=lambda d: SimpleNamespace(**d))

    # Renderiza o HTML como string
    html_string = render_to_string(
        "nutriNow/plano_template.html",
        {
            "plano": plano,
            "dados_json": dados_json_obj
        }
    )

    # Cria um buffer para o PDF
    result = io.BytesIO()

    # Converte o HTML para PDF
    pisa_status = pisa.CreatePDF(
        html_string, dest=result
    )

    if pisa_status.err:
        print("Erro ao gerar PDF")
        return

    plano.arquivo_pdf.save(f"plano_{plano.id}.pdf", ContentFile(result.getvalue()), save=True)
    return plano.arquivo_pdf.path