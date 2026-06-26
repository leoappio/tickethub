using Microsoft.EntityFrameworkCore;
using TicketHub.Application;
using TicketHub.Domain;

namespace TicketHub.Infrastructure;

public class EventService : IEventService
{
    private readonly AppDbContext _db;
    private readonly IEventRepository _repo;

    public EventService(AppDbContext db, IEventRepository repo)
    {
        _db = db;
        _repo = repo;
    }

    public async Task<Guid> CreateAsync(CreateEventRequest req, Guid organizerId)
    {
        var ev = new Event
        {
            Name = req.Name,
            Description = req.Description,
            Venue = req.Venue,
            StartsAt = DateTime.SpecifyKind(req.StartsAt, DateTimeKind.Utc),
            Capacity = req.Capacity,
            OrganizerId = organizerId,
            IsPublished = false
        };
        _db.Events.Add(ev);
        await _db.SaveChangesAsync();
        return ev.Id;
    }

    public async Task<bool> PublishAsync(Guid eventId, Guid organizerId, bool isOrganizerOrAdmin)
    {
        var ev = await _db.Events.FirstOrDefaultAsync(e => e.Id == eventId);
        if (ev is null) return false;
        if (!isOrganizerOrAdmin && ev.OrganizerId != organizerId) return false;
        ev.IsPublished = true;
        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<Guid?> AddTicketTypeAsync(Guid eventId, CreateTicketTypeRequest req)
    {
        var ev = await _db.Events.FirstOrDefaultAsync(e => e.Id == eventId);
        if (ev is null) return null;
        var tt = new TicketType
        {
            EventId = eventId,
            Name = req.Name,
            Price = req.Price,
            Quantity = req.Quantity
        };
        _db.TicketTypes.Add(tt);
        await _db.SaveChangesAsync();
        return tt.Id;
    }

    public async Task<List<EventSummary>> SearchAsync(string? term)
    {
        var events = await _repo.SearchAsync(term);
        return events.Select(Map).ToList();
    }

    public async Task<EventSummary?> GetAsync(Guid id)
    {
        var ev = await _db.Events.AsNoTracking().FirstOrDefaultAsync(e => e.Id == id);
        return ev is null ? null : Map(ev);
    }

    private static EventSummary Map(Event e) =>
        new(e.Id, e.Name, e.Description, e.Venue, e.StartsAt, e.Capacity, e.IsPublished);
}
