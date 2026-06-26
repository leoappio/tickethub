namespace TicketHub.Application;

public record RegisterRequest(string Email, string Password, string FullName);
public record LoginRequest(string Email, string Password);
public record AuthResponse(string AccessToken, string Role, string FullName);

public record CreateEventRequest(
    string Name,
    string Description,
    string Venue,
    DateTime StartsAt,
    int Capacity);

public record CreateTicketTypeRequest(string Name, decimal Price, int Quantity);

public record EventSummary(
    Guid Id,
    string Name,
    string Description,
    string Venue,
    DateTime StartsAt,
    int Capacity,
    bool IsPublished);

public record OrderItemRequest(Guid TicketTypeId, int Quantity);
public record CreateOrderRequest(Guid EventId, List<OrderItemRequest> Items);
public record PayOrderRequest(string CardNumber, string CardCvv, string CardExpiry);

public record OrderResponse(
    Guid Id,
    Guid EventId,
    string Status,
    decimal TotalAmount,
    DateTime CreatedAt);

public record ValidateTicketRequest(string Code);
public record TicketResponse(Guid Id, string Code, string Status, Guid EventId);
