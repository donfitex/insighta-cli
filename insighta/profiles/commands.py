import click
from insighta.utils.request import authenticated_get

@click.group()
def profiles():
    pass


@profiles.command(name="list")
@click.option("--gender", help="Filter by gender")
@click.option("--country", help="Filter by country")
@click.option("--min-age", type=int)
@click.option("--max-age", type=int)
@click.option("--page", default=1)
@click.option("--limit", default=10)
def list_profiles(gender, country, min_age, max_age, page, limit):
    params = {
        "gender": gender,
        "country_id": country,
        "min_age": min_age,
        "max_age": max_age,
        "page": page,
        "limit": limit
    }

    # remove None values
    params = {k: v for k, v in params.items() if v is not None}

    data = authenticated_get("/api/profiles", params)

    if not data:
        return

    print("\n📊 Profiles:\n")

    for p in data.get("data", []):
        print(
            f"{p.get('id')} | {p.get('name')} | {p.get('gender')} | "
            f"{p.get('age')} |{p.get('age_group')} | {p.get('country_name', 'N/A')} | {p.get('country_id', '')} | {p.get('created_at')} "
        )

    print("\n---")
    print(f"Page: {data.get('page')} / {data.get('total_pages')}")
    print(f"Total: {data.get('total')}")





# Profile search command with query parameter and pagination options
@profiles.command(name="search")
@click.argument("query")
@click.option("--page", default=1)
@click.option("--limit", default=10)
def search_profiles(query, page, limit):
    params = {
        "q": query,
        "page": page,
        "limit": limit
    }

    data = authenticated_get("/api/profiles/search", params)

    if not data:
        return

    print(f"\n🔎 Search: {query}\n")


    for p in data.get("data", []):
        print(
            f"{p.get('id')} | {p.get('name')} | {p.get('gender')} | "
            f"{p.get('age')} |{p.get('age_group')} | {p.get('country_name', 'N/A')} | {p.get('country_id', '')} | {p.get('created_at')} "
        )

    print("\n---")
    print(f"Page: {data.get('page')} / {data.get('total_pages')}")
    print(f"Total: {data.get('total')}")