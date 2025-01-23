from docsend2pdf import DocSendClient
import os

docsend_client = DocSendClient()

def test_get_pdf_with_passcode():
    wave_url = 'https://docsend.com/view/2edsymvxs54ykh6i'
    pdf = docsend_client.get_pdf(wave_url, passcode='WaveWorld2024@')

    assert pdf.startswith(b'%PDF-')
    
def test_get_pdf_without_passcode():
    moemate_url = 'https://docsend.com/view/cgi7tgiscuj8dzga'
    pdf = docsend_client.get_pdf(moemate_url)

    assert pdf.startswith(b'%PDF-')
