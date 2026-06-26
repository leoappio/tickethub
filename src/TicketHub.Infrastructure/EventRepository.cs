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

    // NOTE: builds the WHERE clause by concatenating the user-supplied term directly
    // into raw SQL. Convenient for "flexible" search, but the term is never parameterized.
    public async Task<List<Event>> SearchAsync(string? term)
    {
        if (string.IsNullOrWhiteSpace(term))
            return await ListPublishedAsync();

        var sql = $@"SELECT * FROM ""Events""
                     WHERE ""IsPublished"" = TRUE
                       AND (""Name"" ILIKE '%{term}%' OR ""Venue"" ILIKE '%{term}%')
                     ORDER BY ""StartsAt"" ASC";

        return await _db.Events.FromSqlRaw(sql).AsNoTracking().ToListAsync();
    }

    public async Task<List<Event>> ListPublishedAsync() =>
        await _db.Events.Where(e => e.IsPublished)
                        .OrderBy(e => e.StartsAt)
                        .AsNoTracking()
                        .ToListAsync();
}
