using TicketHub.Domain;

namespace TicketHub.Application;

public interface IAuthService
{
    Task<AuthResponse?> RegisterAsync(RegisterRequest req, string ip);
    Task<AuthResponse?> LoginAsync(LoginRequest req, string ip);
}

public interface IEventService
{
    Task<Guid> CreateAsync(CreateEventRequest req, Guid organizerId);
    Task<bool> PublishAsync(Guid eventId, Guid organizerId, bool isOrganizerOrAdmin);
    Task<Guid?> AddTicketTypeAsync(Guid eventId, CreateTicketTypeRequest req);
    Task<List<EventSummary>> SearchAsync(string? term);
    Task<EventSummary?> GetAsync(Guid id);
}

public interface IOrderService
{
    Task<OrderResponse?> CreateAsync(Guid userId, CreateOrderRequest req);
    Task<OrderResponse?> PayAsync(Guid orderId, PayOrderRequest req);
    Task<OrderResponse?> GetAsync(Guid orderId);
}

public interface ITicketService
{
    Task<List<TicketResponse>> ListForOrderAsync(Guid orderId);
    Task<TicketResponse?> ValidateAsync(string code);
}

public interface IReportService
{
    Task<object> SalesSummaryAsync();
}
