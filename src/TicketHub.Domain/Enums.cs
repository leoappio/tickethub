namespace TicketHub.Domain;

public enum UserRole
{
    Customer = 0,
    Organizer = 1,
    Admin = 2
}

public enum OrderStatus
{
    Pending = 0,
    Paid = 1,
    Cancelled = 2,
    Refunded = 3
}

public enum TicketStatus
{
    Valid = 0,
    Used = 1,
    Revoked = 2
}

public enum PaymentStatus
{
    Pending = 0,
    Approved = 1,
    Declined = 2
}
