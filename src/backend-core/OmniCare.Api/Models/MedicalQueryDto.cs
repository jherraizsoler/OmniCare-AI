namespace OmniCare.Api.Models
{
    public class MedicalQueryDto
    {
        public string PatientId { get; set; } = string.Empty;
        public string Symptoms { get; set; } = string.Empty;
        public int UrgencyLevel { get; set; } // 1-5
        public bool ConsentProvided { get; set; }
    }

    public class AiResponseDto
    {
        public string Analysis { get; set; } = string.Empty;
        public List<string> RecommendedActions { get; set; } = new();
        public string AgentInCharge { get; set; } = string.Empty;
    }
}