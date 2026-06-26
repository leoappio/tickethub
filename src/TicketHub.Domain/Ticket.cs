namespace TicketHub.Domain;

public class Ticket
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid OrderId { get; set; }
    public Guid TicketTypeId { get; set; }
    public Guid EventId { get; set; }
    public string Code { get; set; } = string.Empty;
    public TicketStatus Status { get; set; } = TicketStatus.Valid;
    public DateTime IssuedAt { get; set; } = DateTime.UtcNow;
    public DateTime? UsedAt { get; set; }
}
