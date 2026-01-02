using System.Net.Http.Json;
using System.Text.Json;
using OmniCare.Api.Models;

namespace OmniCare.Api.Services
{
    public class AsistenteMedicoService : IAsistenteMedicoService
    {
        private readonly HttpClient _httpClient;
        private readonly JsonSerializerOptions _jsonOptions;

        public AsistenteMedicoService(HttpClient httpClient)
        {
            _httpClient = httpClient;
            // Configuramos las opciones para manejar CamelCase automáticamente
            _jsonOptions = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };
        }

        // Método original (Síncrono para el cliente)
        public async Task<AiResponseDto> AnalizarCasoAsync(MedicalQueryDto consulta)
        {
            var response = await _httpClient.PostAsJsonAsync("analyze", consulta, _jsonOptions);
            response.EnsureSuccessStatusCode();

            return await response.Content.ReadFromJsonAsync<AiResponseDto>(_jsonOptions) 
                   ?? throw new Exception("Error al procesar respuesta de IA");
        }

        // --- NUEVO MÉTODO PARA STREAMING ---
        public async IAsyncEnumerable<string> AnalizarCasoStreamAsync(MedicalQueryDto consulta)
        {
            // Enviamos la petición al nuevo endpoint de streaming en FastAPI
            var response = await _httpClient.PostAsJsonAsync("analyze-stream", consulta, _jsonOptions);
            response.EnsureSuccessStatusCode();

            // Abrimos el stream de respuesta
            using var stream = await response.Content.ReadAsStreamAsync();
            using var reader = new StreamReader(stream);

            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                
                // Los eventos SSE vienen precedidos por "data: "
                if (!string.IsNullOrWhiteSpace(line) && line.StartsWith("data: "))
                {
                    var jsonContent = line.Substring(6); // Extraemos solo el JSON
                    
                    using var doc = JsonDocument.Parse(jsonContent);
                    if (doc.RootElement.TryGetProperty("token", out var tokenElement))
                    {
                        yield return tokenElement.GetString() ?? "";
                    }
                }
            }
        }
    }
}