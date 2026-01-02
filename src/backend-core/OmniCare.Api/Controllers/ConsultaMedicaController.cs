using Microsoft.AspNetCore.Mvc;
using OmniCare.Api.Models;
using OmniCare.Api.Services;

namespace OmniCare.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ConsultaMedicaController : ControllerBase
    {
        private readonly IAsistenteMedicoService _aiService;
        private readonly ILogger<ConsultaMedicaController> _logger;

        public ConsultaMedicaController(IAsistenteMedicoService aiService, ILogger<ConsultaMedicaController> logger)
        {
            _aiService = aiService;
            _logger = logger;
        }

        /// <summary>
        /// Envía una consulta médica al motor de IA para su análisis.
        /// </summary>
        /// <param name="consulta">Datos del paciente y síntomas.</param>
        /// <returns>Análisis generado por los agentes de LangGraph.</returns>
        [HttpPost("analizar")]
        [ProducesResponseType(typeof(AiResponseDto), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<IActionResult> Analizar([FromBody] MedicalQueryDto consulta)
        {
            // 1. Validación de Reglas de Negocio (Diseño Sólido)
            if (!consulta.ConsentProvided)
            {
                _logger.LogWarning("Intento de consulta sin consentimiento para el paciente: {PatientId}", consulta.PatientId);
                return BadRequest("Se requiere el consentimiento explícito del paciente para procesar datos médicos.");
            }

            if (string.IsNullOrWhiteSpace(consulta.Symptoms))
            {
                return BadRequest("La descripción de los síntomas no puede estar vacía.");
            }

            try
            {
                _logger.LogInformation("Enviando caso del paciente {PatientId} al motor de IA...", consulta.PatientId);

                // 2. Llamada al Puente (Python FastAPI)
                var resultado = await _aiService.AnalizarCasoAsync(consulta);

                return Ok(resultado);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error al comunicarse con el motor de IA para el paciente {PatientId}", consulta.PatientId);
                return StatusCode(500, "Error interno al procesar el análisis médico.");
            }
        }
    }
}