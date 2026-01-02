using System.Net.Http.Json;
using OmniCare.Api.Models;

namespace OmniCare.Api.Services
{
    public class AsistenteMedicoService : IAsistenteMedicoService
    {
        private readonly HttpClient _httpClient;

        public AsistenteMedicoService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<AiResponseDto> AnalizarCasoAsync(MedicalQueryDto consulta)
        {
            // Llamada al microservicio de Python (FastAPI)
            var response = await _httpClient.PostAsJsonAsync("analyze", consulta);
            response.EnsureSuccessStatusCode();

            return await response.Content.ReadFromJsonAsync<AiResponseDto>() 
                   ?? throw new Exception("Error al procesar respuesta de IA");
        }
    }
}