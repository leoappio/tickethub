using System.Security.Cryptography;

namespace TicketHub.Application;

public interface IPasswordService
{
    string Hash(string password);
    bool Verify(string password, string hash);
}

// PBKDF2 (RFC 2898) with a per-user random salt. Hash format:
//   pbkdf2$<iterations>$<base64-salt>$<base64-subkey>
public class PasswordService : IPasswordService
{
    private const int Iterations = 210_000;     // OWASP 2023 guidance for PBKDF2-HMAC-SHA256
    private const int SaltSize = 16;            // 128-bit salt
    private const int KeySize = 32;             // 256-bit derived key
    private static readonly HashAlgorithmName Algorithm = HashAlgorithmName.SHA256;

    public string Hash(string password)
    {
        var salt = RandomNumberGenerator.GetBytes(SaltSize);
        var subkey = Rfc2898DeriveBytes.Pbkdf2(password, salt, Iterations, Algorithm, KeySize);
        return $"pbkdf2${Iterations}${Convert.ToBase64String(salt)}${Convert.ToBase64String(subkey)}";
    }

    public bool Verify(string password, string hash)
    {
        var parts = hash.Split('$');
        if (parts.Length != 4 || parts[0] != "pbkdf2") return false;
        if (!int.TryParse(parts[1], out var iterations)) return false;

        var salt = Convert.FromBase64String(parts[2]);
        var expected = Convert.FromBase64String(parts[3]);
        var actual = Rfc2898DeriveBytes.Pbkdf2(password, salt, iterations, Algorithm, expected.Length);

        // Constant-time comparison to avoid timing side channels.
        return CryptographicOperations.FixedTimeEquals(actual, expected);
    }
}
