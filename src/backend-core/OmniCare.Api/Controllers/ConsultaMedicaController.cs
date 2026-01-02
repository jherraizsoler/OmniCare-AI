using Microsoft.AspNetCore.Mvc;
using OmniCare.Api.Models;
using OmniCare.Api.Services;

namespace OmniCare.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ConsultaMedicaController : ControllerBase
    {
        private readonly IAsistenteMedicoService _asistenteService;
        private readonly ILogger<ConsultaMedicaController> _logger;

        public ConsultaMedicaController(IAsistenteMedicoService asistenteService, ILogger<ConsultaMedicaController> logger)
        {
            _asistenteService = asistenteService;
            _logger = logger;
        }

        // Endpoint de Streaming
        [HttpPost("analizar-stream")]
        public async Task AnalizarStream([FromBody] MedicalQueryDto consulta)
        {
            // Validamos consentimiento antes de iniciar el flujo
            if (!consulta.ConsentProvided)
            {
                _logger.LogWarning("Intento de consulta sin consentimiento para el paciente: {PatientId}", consulta.PatientId);
                Response.StatusCode = 400;
                await Response.WriteAsync("Se requiere el consentimiento del paciente.");
                return;
            }

            _logger.LogInformation("Iniciando streaming de IA para el paciente {PatientId}...", consulta.PatientId);

            // Establecemos el tipo de contenido como texto plano para el stream
            Response.ContentType = "text/plain";

            try
            {
                // Consumimos el IAsyncEnumerable de nuestro servicio
                await foreach (var token in _asistenteService.AnalizarCasoStreamAsync(consulta))
                {
                    // Escribimos el token directamente en el cuerpo de la respuesta HTTP
                    await Response.WriteAsync(token);
                    
                    // Forzamos el envío del buffer para que el cliente vea la palabra de inmediato
                    await Response.Body.FlushAsync();
                }
                
                _logger.LogInformation("Streaming completado con éxito para {PatientId}", consulta.PatientId);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error durante el streaming de IA para el paciente {PatientId}", consulta.PatientId);
                Response.StatusCode = 500;
            }
        }
    }
}