from core.email_service import send_email_using_default_email
import traceback

class APIErrorAlertMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        tb = traceback.format_exc()

        try:
            status = send_email_using_default_email(
                to_email='mqamartech@gmail.com',
                subject=f'500 Error on {request.path}',
                body= 'A 500 error just happened on your API.',
                html_message=f'''
                    A 500 error just happened on your API.<br><br>
                    <b>Path:</b> {request.path}<br>
                    <b>Method:</b> {request.method}<br>
                    <b>Error:</b> {str(exception)}<br><br>
                    <b>Traceback:</b><br>
                    <pre>{tb}</pre>
                '''
            )
            print(f"Alert email sent — status: {status}")
        except Exception as e:
            print(f"Failed to send alert email: {e}")

        return None