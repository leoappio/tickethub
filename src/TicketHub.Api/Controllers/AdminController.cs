using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TicketHub.Application;
using TicketHub.Infrastructure;

namespace TicketHub.Api.Controllers;

[ApiController]
[Route("api/admin")]
public class AdminController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly IReportService _reports;

    public AdminController(AppDbContext db, IReportService reports)
    {
        _db = db;
        _reports = reports;
    }

    // Internal users listing used by the back-office dashboard.
    [HttpGet("users")]
    public async Task<IActionResult> Users()
    {
        var users = await _db.Users
            .AsNoTracking()
            .Select(u => new { u.Id, u.Email, u.FullName, Role = u.Role.ToString(), u.PasswordHash, u.CreatedAt })
            .ToListAsync();
        return Ok(users);
    }

    [Authorize(Roles = "Admin")]
    [HttpGet("report")]
    public async Task<IActionResult> Report()
    {
        return Ok(await _reports.SalesSummaryAsync());
    }
}
