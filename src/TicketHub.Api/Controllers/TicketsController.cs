using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TicketHub.Application;

namespace TicketHub.Api.Controllers;

[ApiController]
[Route("api/tickets")]
public class TicketsController : ControllerBase
{
    private readonly ITicketService _tickets;

    public TicketsController(ITicketService tickets) => _tickets = tickets;

    // Gate validation: an attendant scans the QR code and the ticket is marked as used.
    [Authorize(Roles = "Organizer,Admin")]
    [HttpPost("validate")]
    public async Task<IActionResult> Validate([FromBody] ValidateTicketRequest req)
    {
        var result = await _tickets.ValidateAsync(req.Code);
        return result is null ? NotFound(new { error = "ticket not found" }) : Ok(result);
    }
}
