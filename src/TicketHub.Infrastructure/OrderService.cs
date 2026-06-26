using Microsoft.EntityFrameworkCore;
using TicketHub.Application;
using TicketHub.Domain;

namespace TicketHub.Infrastructure;

public class OrderService : IOrderService
{
    private readonly AppDbContext _db;

    public OrderService(AppDbContext db) => _db = db;

    public async Task<OrderResponse?> CreateAsync(Guid userId, CreateOrderRequest req)
    {
        if (req.Items is null || req.Items.Count == 0) return null;

        var typeIds = req.Items.Select(i => i.TicketTypeId).ToList();
        var types = await _db.TicketTypes
            .Where(t => typeIds.Contains(t.Id) && t.EventId == req.EventId)
            .ToListAsync();

        if (types.Count != typeIds.Distinct().Count()) return null;

        var order = new Order { UserId = userId, EventId = req.EventId, Status = OrderStatus.Pending };
        decimal total = 0m;

        foreach (var item in req.Items)
        {
            var type = types.First(t => t.Id == item.TicketTypeId);
            if (item.Quantity <= 0 || item.Quantity > type.Available)
                return null; // business rule: cannot oversell

            type.SoldCount += item.Quantity; // reserve
            order.Items.Add(new OrderItem
            {
                TicketTypeId = type.Id,
                Quantity = item.Quantity,
                UnitPrice = type.Price
            });
            total += type.Price * item.Quantity;
        }

        order.TotalAmount = total;
        _db.Orders.Add(order);
        await _db.SaveChangesAsync();
        return Map(order);
    }

    public async Task<OrderResponse?> PayAsync(Guid orderId, PayOrderRequest req)
    {
        var order = await _db.Orders
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == orderId);

        if (order is null || order.Status != OrderStatus.Pending) return null;

        var digits = new string(req.CardNumber.Where(char.IsDigit).ToArray());
        var approved = digits.Length is >= 13 and <= 19;

        var payment = new Payment
        {
            OrderId = order.Id,
            Amount = order.TotalAmount,
            Method = "card",
            CardLast4 = digits.Length >= 4 ? digits[^4..] : digits,
            Status = approved ? PaymentStatus.Approved : PaymentStatus.Declined
        };
        _db.Payments.Add(payment);

        if (!approved)
        {
            await _db.SaveChangesAsync();
            return Map(order);
        }

        order.Status = OrderStatus.Paid;

        foreach (var item in order.Items)
        {
            for (var i = 0; i < item.Quantity; i++)
            {
                _db.Tickets.Add(new Ticket
                {
                    OrderId = order.Id,
                    TicketTypeId = item.TicketTypeId,
                    EventId = order.EventId,
                    Code = $"TH-{Guid.NewGuid():N}"[..16].ToUpperInvariant(),
                    Status = TicketStatus.Valid
                });
            }
        }

        await _db.SaveChangesAsync();
        return Map(order);
    }

    public async Task<OrderResponse?> GetAsync(Guid orderId)
    {
        var order = await _db.Orders.AsNoTracking().FirstOrDefaultAsync(o => o.Id == orderId);
        return order is null ? null : Map(order);
    }

    private static OrderResponse Map(Order o) =>
        new(o.Id, o.EventId, o.Status.ToString(), o.TotalAmount, o.CreatedAt);
}
