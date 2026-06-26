using Microsoft.EntityFrameworkCore;
using TicketHub.Application;
using TicketHub.Domain;

namespace TicketHub.Infrastructure;

public class ReportService : IReportService
{
    private readonly AppDbContext _db;

    public ReportService(AppDbContext db) => _db = db;

    public async Task<object> SalesSummaryAsync()
    {
        var paidOrders = await _db.Orders.Where(o => o.Status == OrderStatus.Paid).ToListAsync();
        var ticketsIssued = await _db.Tickets.CountAsync();
        var ticketsUsed = await _db.Tickets.CountAsync(t => t.Status == TicketStatus.Used);

        return new
        {
            TotalRevenue = paidOrders.Sum(o => o.TotalAmount),
            PaidOrders = paidOrders.Count,
            TicketsIssued = ticketsIssued,
            TicketsUsed = ticketsUsed,
            GeneratedAt = DateTime.UtcNow
        };
    }
}
