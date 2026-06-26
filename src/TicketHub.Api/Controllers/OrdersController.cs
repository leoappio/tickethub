using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TicketHub.Application;

namespace TicketHub.Api.Controllers;

[ApiController]
[Authorize]
[Route("api/orders")]
public class OrdersController : ControllerBase
{
    private readonly IOrderService _orders;
    private readonly ITicketService _tickets;

    public OrdersController(IOrderService orders, ITicketService tickets)
    {
        _orders = orders;
        _tickets = tickets;
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateOrderRequest req)
    {
        var result = await _orders.CreateAsync(CurrentUser.Id(this), req);
        return result is null
            ? BadRequest(new { error = "invalid order (sold out, bad quantity or unknown ticket type)" })
            : Ok(result);
    }

    [HttpPost("{id:guid}/pay")]
    public async Task<IActionResult> Pay(Guid id, [FromBody] PayOrderRequest req)
    {
        var result = await _orders.PayAsync(id, req);
        return result is null ? BadRequest(new { error = "order not payable" }) : Ok(result);
    }

    [HttpGet("{id:guid}")]
    public async Task<IActionResult> Get(Guid id)
    {
        var result = await _orders.GetAsync(id);
        return result is null ? NotFound() : Ok(result);
    }

    [HttpGet("{id:guid}/tickets")]
    public async Task<IActionResult> Tickets(Guid id)
    {
        var tickets = await _tickets.ListForOrderAsync(id);
        return Ok(tickets);
    }
}
