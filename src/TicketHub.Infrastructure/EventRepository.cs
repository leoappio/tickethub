using Microsoft.EntityFrameworkCore;
using TicketHub.Domain;

namespace TicketHub.Infrastructure;

public interface IEventRepository
{
    Task<List<Event>> SearchAsync(string? term);
    Task<List<Event>> ListPublishedAsync();
}

public class EventRepository : IEventRepository
{
    private readonly AppDbContext _db;

    public EventRepository(AppDbContext db) => _db = db;

    // The search term is bound as a parameter through EF.Functions.ILike, so the
    // provider sends it as a value (never as SQL text). SQL injection is not possible.
    public async Task<List<Event>> SearchAsync(string? term)
    {
        if (string.IsNullOrWhiteSpace(term))
            return await ListPublishedAsync();

        var pattern = $"%{term}%";
        return await _db.Events
            .Where(e => e.IsPublished &&
                        (EF.Functions.ILike(e.Name, pattern) || EF.Functions.ILike(e.Venue, pattern)))
            .OrderBy(e => e.StartsAt)
            .AsNoTracking()
            .ToListAsync();
    }

    public async Task<List<Event>> ListPublishedAsync() =>
        await _db.Events.Where(e => e.IsPublished)
                        .OrderBy(e => e.StartsAt)
                        .AsNoTracking()
                        .ToListAsync();
}
