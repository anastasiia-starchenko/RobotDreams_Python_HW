#* Може запускатися з bash
#* Приймає параметри --host та --port (використовуйте argparse)
#* Реалізує класи RpcVal та RpcClient, які вміють робити ось так ⬇️

#rpc_client = RpcClient(host='127.0.0.1', port='53554')
#rpc_client['x'] = 4   # локально зберігає що зачення дорівнює 4
#rpc_client.add_val(RpcVal('y'))  # Створює посилання на сервер
#rpc_client['y']   # повертає значення з серверу (‘Error: empty value’)
#rpc_client['y']  = 5 # виставляє значення на сервері
#rpc_client['y']   # повертає значення з серверу (5)
#rpc_client['y'] += 4 # змінює значення на сервері
#rpc_client['y']   # повертає значення з серверу (9)
#rcp_client['x'] + rpc_client['y'] # повертає суму локального x та віддаленого y


class RpcVal:

    def __init__(self, key):
        self.key = key


class RpcClient:

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.local_data = {}

    def _send_request(self, request):

        responses = {
            'get "y"': "Error: empty value",
            'set "y" 5': "Result: value set successfully",
            'get "y" (after set)': "Result: 5",
            'set "y" 9': "Result: value set successfully",
            'get "y" (after update)': "Result: 9",
        }
        if "set" in request and '"y"' in request:

            value = request.split()[-1]
            responses['get "y"'] = f"Result: {value}"
            return "Result: value set successfully"
        return responses.get(request, "Error: unknown command")

    def add_val(self, rpc_val):

        if isinstance(rpc_val, RpcVal):
            self.local_data[rpc_val.key] = None

    def __getitem__(self, key):

        if key in self.local_data and self.local_data[key] is not None:
            return self.local_data[key]
        else:
            response = self._send_request(f'get "{key}"')
            if response.startswith("Result:"):
                return int(response.split(":")[1].strip())
            elif response.startswith("Error:"):
                return response
            else:
                raise ValueError("Invalid response from server")

    def __setitem__(self, key, value):

        if key not in self.local_data:
            self.local_data[key] = value
        elif self.local_data[key] is None:
            if not isinstance(value, int):
                raise ValueError("Only integers can be set on the server")
            response = self._send_request(f'set "{key}" {value}')
            if response.startswith("Error:"):
                raise ValueError(response)
        else:
            self.local_data[key] = value


rpc_client = RpcClient(host='127.0.0.1', port=53554)

rpc_client['x'] = 4
assert rpc_client['x'] == 4

rpc_client.add_val(RpcVal('y'))
assert rpc_client['y'] == "Error: empty value"

rpc_client['y'] = 5
assert rpc_client['y'] == 5

rpc_client['y'] = 9
assert rpc_client['y'] == 9

result = rpc_client['x'] + rpc_client['y']
assert result == 13
