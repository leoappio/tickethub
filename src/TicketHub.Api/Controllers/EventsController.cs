using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TicketHub.Application;

namespace TicketHub.Api.Controllers;

[ApiController]
[Route("api/events")]
public class EventsController : ControllerBase
{
    private readonly IEventService _events;

    public EventsController(IEventService events) => _events = events;

    [HttpGet("{id:guid}")]
    public async Task<IActionResult> Get(Guid id)
    {
        var ev = await _events.GetAsync(id);
        return ev is null ? NotFound() : Ok(ev);
    }

    [HttpGet("search")]
    public async Task<IActionResult> Search([FromQuery] string? q)
    {
        var results = await _events.SearchAsync(q);
        return Ok(results);
    }

    [Authorize(Roles = "Organizer,Admin")]
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateEventRequest req)
    {
        var id = await _events.CreateAsync(req, CurrentUser.Id(this));
        return CreatedAtAction(nameof(Get), new { id }, new { id });
    }

    [Authorize(Roles = "Organizer,Admin")]
    [HttpPost("{id:guid}/ticket-types")]
    public async Task<IActionResult> AddTicketType(Guid id, [FromBody] CreateTicketTypeRequest req)
    {
        var ttId = await _events.AddTicketTypeAsync(id, req);
        return ttId is null ? NotFound() : Ok(new { id = ttId });
    }

    [Authorize(Roles = "Organizer,Admin")]
    [HttpPost("{id:guid}/publish")]
    public async Task<IActionResult> Publish(Guid id)
    {
        var ok = await _events.PublishAsync(id, CurrentUser.Id(this), CurrentUser.IsOrganizerOrAdmin(this));
        return ok ? Ok(new { published = true }) : NotFound();
    }
}
