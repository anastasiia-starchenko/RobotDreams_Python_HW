
import asyncio

data = {}


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Підключено: {addr}")

    while True:
        request = await reader.read(1024)
        if not request:
            break

        request_text = request.decode('utf-8').strip()
        print(f"Отримано запит: {request_text}")
        response = await handle_request(request_text)

        writer.write(response.encode('utf-8'))
        await writer.drain()

    writer.close()
    await writer.wait_closed()
    print(f"З'єднання закрито: {addr}")


async def handle_request(request):
    parts = request.split(' ', 2)
    command = parts[0].lower()

    if command == "get":
        if len(parts) != 2:
            return "Error: invalid get command"
        key = parts[1].strip('"')
        value = data.get(key)
        return f"Result: {value}" if value is not None else "Error: empty value"

    elif command == "set":
        if len(parts) != 3:
            return "Error: invalid set command"
        key = parts[1].strip('"')
        value = parts[2]
        if value.isdigit():
            data[key] = int(value)
            return "Result: value set successfully"
        else:
            return "Error: not a number"

    elif command == "getkeys":
        keys = ', '.join(data.keys())
        return f"Result: {keys}" if keys else "Error: no keys in data"

    else:
        return "Error: unknown command"


async def start_server(host="127.0.0.1", port=53554):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"RPC сервер запущено на {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(start_server())
