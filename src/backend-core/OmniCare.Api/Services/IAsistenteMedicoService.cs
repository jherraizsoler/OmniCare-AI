using OmniCare.Api.Models;

namespace OmniCare.Api.Services
{
    public interface IAsistenteMedicoService
    {
        Task<AiResponseDto> AnalizarCasoAsync(MedicalQueryDto consulta);
    }
}