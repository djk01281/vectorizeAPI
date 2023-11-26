import httpx

async def download_image(url: str, local_path: str) -> None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url)

        # Check if the server returns an HTTPException
        if response.status_code == 409 or response.status_code == 403 and response.headers.get("content-type", "").startswith("image/x-icon"):
            print("Skipping favicon request")
            return

        if response.status_code == 200:
            # Process the response as needed
            # ...
            print("Success")
            return
        else:
            # Print a message for non-successful status codes
            print(f"Failed to download image from {url}. Status code: {response.status_code}")

# Example usage in an asynchronous function
async def main() -> None:
    url_input = 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-VAeEgLgTC49WEhK5uy3xPxRD/user-OlLjlSJ02XN7ULb70X650iTm/img-FIUaTQsH4lTNO5R9AV9ENBbp.png?st=2023-11-23T10%3A57%3A37Z&se=2023-11-23T12%3A57%3A37Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-11-23T06%3A31%3A04Z&ske=2023-11-24T06%3A31%3A04Z&sks=b&skv=2021-08-06&sig=dykz0qpTsr1IuGZxA7v1%2B/7QSoK/pG97cslLm7ygFWg%3D'
    input_path = "./input.png"
    await download_image(url_input, input_path)

# Run the event loop
import asyncio
asyncio.run(main())
