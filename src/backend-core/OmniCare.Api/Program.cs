using OmniCare.Api.Services;
using Scalar.AspNetCore; // Añade esto

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddOpenApi(); // Esto ya lo tienes

builder.Services.AddHttpClient<IAsistenteMedicoService, AsistenteMedicoService>(client =>
{
    client.BaseAddress = new Uri("http://localhost:8000/");
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi(); // El motor
    app.MapScalarApiReference(); // La interfaz visual (en lugar de Swagger)
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();