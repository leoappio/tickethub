FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY Directory.Build.props ./
COPY src/TicketHub.Domain/TicketHub.Domain.csproj src/TicketHub.Domain/
COPY src/TicketHub.Application/TicketHub.Application.csproj src/TicketHub.Application/
COPY src/TicketHub.Infrastructure/TicketHub.Infrastructure.csproj src/TicketHub.Infrastructure/
COPY src/TicketHub.Api/TicketHub.Api.csproj src/TicketHub.Api/
RUN dotnet restore src/TicketHub.Api/TicketHub.Api.csproj

COPY . .
RUN dotnet publish src/TicketHub.Api/TicketHub.Api.csproj -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .

# Run as a non-root, unprivileged user.
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app
USER 10001

ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
    CMD ["sh", "-c", "wget -qO- http://127.0.0.1:8080/health || exit 1"]

ENTRYPOINT ["dotnet", "TicketHub.Api.dll"]
