namespace TicketHub.Domain;

public class LoginLog
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid? UserId { get; set; }
    public string Email { get; set; } = string.Empty;
    public bool Success { get; set; }
    public string IpAddress { get; set; } = string.Empty;
    public DateTime At { get; set; } = DateTime.UtcNow;
}
