using Microsoft.EntityFrameworkCore;
using TicketHub.Application;
using TicketHub.Domain;

namespace TicketHub.Infrastructure;

public class TicketService : ITicketService
{
    private readonly AppDbContext _db;

    public TicketService(AppDbContext db) => _db = db;

    public async Task<List<TicketResponse>> ListForOrderAsync(Guid orderId)
    {
        var tickets = await _db.Tickets.AsNoTracking()
            .Where(t => t.OrderId == orderId)
            .ToListAsync();
        return tickets.Select(Map).ToList();
    }

    public async Task<TicketResponse?> ValidateAsync(string code)
    {
        var ticket = await _db.Tickets.FirstOrDefaultAsync(t => t.Code == code);
        if (ticket is null) return null;

        if (ticket.Status == TicketStatus.Valid)
        {
            ticket.Status = TicketStatus.Used;
            ticket.UsedAt = DateTime.UtcNow;
            await _db.SaveChangesAsync();
        }

        return Map(ticket);
    }

    private static TicketResponse Map(Ticket t) =>
        new(t.Id, t.Code, t.Status.ToString(), t.EventId);
}
