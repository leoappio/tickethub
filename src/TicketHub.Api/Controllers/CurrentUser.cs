using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using Microsoft.AspNetCore.Mvc;

namespace TicketHub.Api.Controllers;

public static class CurrentUser
{
    public static Guid Id(ControllerBase c)
    {
        var sub = c.User.FindFirstValue(JwtRegisteredClaimNames.Sub)
                  ?? c.User.FindFirstValue(ClaimTypes.NameIdentifier);
        return Guid.TryParse(sub, out var id) ? id : Guid.Empty;
    }

    public static bool IsOrganizerOrAdmin(ControllerBase c) =>
        c.User.IsInRole("Organizer") || c.User.IsInRole("Admin");
}
