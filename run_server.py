import config

cmd = """docker run -it --rm -p %PORT%:8500 -v "{}/serving_model/%MODEL_NAME%:/models/%MODEL_NAME%" -e MODEL_NAME=%MODEL_NAME% tensorflow/serving:1.15.0-gpu
""".format(config.PATH)

model = [[i, name] for i, name in enumerate(config.model_api)]
msg = "\n".join(["{}. {}".format(i + 1, name) for i, name in enumerate(config.model_api)])

print(msg)

idx = int(input("Enter index: ")) - 1

if 0 <= idx < len(config.model_api):
    model = [i for i in config.model_api.keys()][idx]
    port = config.model_api[model]
    command = cmd.replace("%MODEL_NAME%", model).replace("%PORT%", port)
    print(command)
    print("run model {} on port {}".format(model, port))