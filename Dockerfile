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

ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080

ENTRYPOINT ["dotnet", "TicketHub.Api.dll"]
