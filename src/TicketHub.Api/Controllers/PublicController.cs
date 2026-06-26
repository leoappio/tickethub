using System.Text;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Mvc;
using TicketHub.Application;

namespace TicketHub.Api.Controllers;

[ApiController]
[Route("public")]
public class PublicController : ControllerBase
{
    private readonly IEventService _events;

    public PublicController(IEventService events) => _events = events;

    // Public, server-rendered event listing with a search box.
    [HttpGet("events")]
    public async Task<ContentResult> Events([FromQuery] string? search)
    {
        var events = await _events.SearchAsync(search);
        var enc = HtmlEncoder.Default;

        var sb = new StringBuilder();
        sb.Append("<!doctype html><html><head><title>TicketHub — Events</title></head><body>");
        sb.Append("<h1>Upcoming events</h1>");
        sb.Append("<form method=\"get\" action=\"/public/events\">");
        sb.Append("<input name=\"search\" placeholder=\"search events\" value=\"")
          .Append(enc.Encode(search ?? string.Empty)).Append("\"/>");
        sb.Append("<button type=\"submit\">Search</button></form>");

        if (!string.IsNullOrEmpty(search))
            sb.Append("<p>Results for: ").Append(enc.Encode(search)).Append("</p>");

        sb.Append("<ul>");
        foreach (var e in events)
        {
            sb.Append("<li><strong>").Append(enc.Encode(e.Name)).Append("</strong> — ")
              .Append(enc.Encode(e.Venue)).Append("<br/>")
              .Append(enc.Encode(e.Description)).Append("</li>");
        }
        sb.Append("</ul></body></html>");

        return new ContentResult
        {
            Content = sb.ToString(),
            ContentType = "text/html",
            StatusCode = 200
        };
    }
}
