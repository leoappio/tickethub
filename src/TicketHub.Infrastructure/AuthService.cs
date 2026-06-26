using Microsoft.EntityFrameworkCore;
using TicketHub.Application;
using TicketHub.Domain;

namespace TicketHub.Infrastructure;

public class AuthService : IAuthService
{
    private readonly AppDbContext _db;
    private readonly IPasswordService _passwords;
    private readonly ITokenService _tokens;

    public AuthService(AppDbContext db, IPasswordService passwords, ITokenService tokens)
    {
        _db = db;
        _passwords = passwords;
        _tokens = tokens;
    }

    public async Task<AuthResponse?> RegisterAsync(RegisterRequest req, string ip)
    {
        var exists = await _db.Users.AnyAsync(u => u.Email == req.Email);
        if (exists) return null;

        var user = new User
        {
            Email = req.Email.Trim().ToLowerInvariant(),
            FullName = req.FullName,
            PasswordHash = _passwords.Hash(req.Password),
            Role = UserRole.Customer
        };

        _db.Users.Add(user);
        await _db.SaveChangesAsync();

        return new AuthResponse(_tokens.CreateAccessToken(user), user.Role.ToString(), user.FullName);
    }

    public async Task<AuthResponse?> LoginAsync(LoginRequest req, string ip)
    {
        var email = req.Email.Trim().ToLowerInvariant();
        var user = await _db.Users.FirstOrDefaultAsync(u => u.Email == email);
        var ok = user is not null && user.IsActive && _passwords.Verify(req.Password, user.PasswordHash);

        _db.LoginLogs.Add(new LoginLog
        {
            UserId = user?.Id,
            Email = email,
            Success = ok,
            IpAddress = ip
        });
        await _db.SaveChangesAsync();

        if (!ok || user is null) return null;
        return new AuthResponse(_tokens.CreateAccessToken(user), user.Role.ToString(), user.FullName);
    }
}
