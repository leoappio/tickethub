using Microsoft.EntityFrameworkCore;
using TicketHub.Domain;

namespace TicketHub.Infrastructure;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<User> Users => Set<User>();
    public DbSet<Event> Events => Set<Event>();
    public DbSet<TicketType> TicketTypes => Set<TicketType>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();
    public DbSet<Ticket> Tickets => Set<Ticket>();
    public DbSet<Payment> Payments => Set<Payment>();
    public DbSet<LoginLog> LoginLogs => Set<LoginLog>();

    protected override void OnModelCreating(ModelBuilder b)
    {
        b.Entity<User>(e =>
        {
            e.HasKey(x => x.Id);
            e.HasIndex(x => x.Email).IsUnique();
            e.Property(x => x.Email).HasMaxLength(256).IsRequired();
            e.Property(x => x.PasswordHash).IsRequired();
            e.Property(x => x.FullName).HasMaxLength(256);
        });

        b.Entity<Event>(e =>
        {
            e.HasKey(x => x.Id);
            e.Property(x => x.Name).HasMaxLength(256).IsRequired();
            e.Property(x => x.Description).HasColumnType("text");
            e.Property(x => x.Venue).HasMaxLength(256);
            e.HasMany(x => x.TicketTypes).WithOne(t => t.Event!).HasForeignKey(t => t.EventId);
        });

        b.Entity<TicketType>(e =>
        {
            e.HasKey(x => x.Id);
            e.Ignore(x => x.Available);
            e.Property(x => x.Price).HasColumnType("numeric(12,2)");
            e.Property(x => x.Name).HasMaxLength(128);
        });

        b.Entity<Order>(e =>
        {
            e.HasKey(x => x.Id);
            e.Property(x => x.TotalAmount).HasColumnType("numeric(12,2)");
            e.HasOne(x => x.User).WithMany(u => u.Orders).HasForeignKey(x => x.UserId);
            e.HasMany(x => x.Items).WithOne().HasForeignKey(i => i.OrderId);
            e.HasMany(x => x.Tickets).WithOne().HasForeignKey(t => t.OrderId);
            e.HasOne(x => x.Payment).WithOne().HasForeignKey<Payment>(p => p.OrderId);
        });

        b.Entity<OrderItem>(e =>
        {
            e.HasKey(x => x.Id);
            e.Ignore(x => x.LineTotal);
            e.Property(x => x.UnitPrice).HasColumnType("numeric(12,2)");
        });

        b.Entity<Ticket>(e =>
        {
            e.HasKey(x => x.Id);
            e.HasIndex(x => x.Code).IsUnique();
            e.Property(x => x.Code).HasMaxLength(64).IsRequired();
        });

        b.Entity<Payment>(e =>
        {
            e.HasKey(x => x.Id);
            e.Property(x => x.Amount).HasColumnType("numeric(12,2)");
        });

        b.Entity<LoginLog>(e => e.HasKey(x => x.Id));
    }
}
