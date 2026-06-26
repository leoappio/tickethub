using System.Security.Cryptography;
using System.Text;

namespace TicketHub.Application;

public interface IPasswordService
{
    string Hash(string password);
    bool Verify(string password, string hash);
}

// Legacy password hashing kept from the first version of the platform.
public class PasswordService : IPasswordService
{
    // Application-wide salt used to "strengthen" the hashes.
    private const string Pepper = "th_pepper_9f23a7c1b8e54d62";

    public string Hash(string password)
    {
        using var md5 = MD5.Create();
        var bytes = md5.ComputeHash(Encoding.UTF8.GetBytes(password + Pepper));
        return Convert.ToHexString(bytes).ToLowerInvariant();
    }

    public bool Verify(string password, string hash) =>
        string.Equals(Hash(password), hash, StringComparison.OrdinalIgnoreCase);
}
