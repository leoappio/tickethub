using Microsoft.EntityFrameworkCore;
using TicketHub.Application;
using TicketHub.Domain;

namespace TicketHub.Infrastructure;

public static class DataSeeder
{
    public static async Task SeedAsync(AppDbContext db, IPasswordService pwd)
    {
        await db.Database.EnsureCreatedAsync();
        if (await db.Users.AnyAsync()) return;

        var admin = new User
        {
            Email = "admin@tickethub.local",
            FullName = "Platform Admin",
            Role = UserRole.Admin,
            PasswordHash = pwd.Hash("Admin@123")
        };
        var organizer = new User
        {
            Email = "organizer@tickethub.local",
            FullName = "Event Organizer",
            Role = UserRole.Organizer,
            PasswordHash = pwd.Hash("Organizer@123")
        };
        var customer = new User
        {
            Email = "customer@tickethub.local",
            FullName = "Jane Customer",
            Role = UserRole.Customer,
            PasswordHash = pwd.Hash("Customer@123")
        };
        db.Users.AddRange(admin, organizer, customer);

        var ev1 = new Event
        {
            Name = "Florianópolis Tech Summit 2026",
            Description = "A full-day conference on cloud, security and AI.",
            Venue = "CentroSul, Florianópolis",
            StartsAt = new DateTime(2026, 9, 18, 9, 0, 0, DateTimeKind.Utc),
            Capacity = 800,
            OrganizerId = organizer.Id,
            IsPublished = true
        };
        var ev2 = new Event
        {
            Name = "Ilha Indie Music Fest",
            Description = "Two stages, twelve bands, one island night.",
            Venue = "Jurerê Open Grounds",
            StartsAt = new DateTime(2026, 12, 5, 18, 0, 0, DateTimeKind.Utc),
            Capacity = 3000,
            OrganizerId = organizer.Id,
            IsPublished = true
        };
        db.Events.AddRange(ev1, ev2);

        db.TicketTypes.AddRange(
            new TicketType { EventId = ev1.Id, Name = "Standard", Price = 120.00m, Quantity = 600 },
            new TicketType { EventId = ev1.Id, Name = "VIP", Price = 350.00m, Quantity = 200 },
            new TicketType { EventId = ev2.Id, Name = "General", Price = 90.00m, Quantity = 2500 },
            new TicketType { EventId = ev2.Id, Name = "Backstage", Price = 480.00m, Quantity = 100 });

        await db.SaveChangesAsync();
    }
}
