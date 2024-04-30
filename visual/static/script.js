function highlightEntities(entities) {
    var text = document.getElementById('inputText').value;
    entities.forEach(function (entity) {
        var re = new RegExp(entity.entity, 'g');
        var type = entity.type;
        var confidence = entity.confidence;
        var color = entity.color;
        text = text.replace(re, '<span class="entity" style="background-color:' + color + ';" title="Type: ' + type + ', Confidence: ' + confidence.toFixed(2) + '">' + entity.entity + '</span>');
    });
    document.getElementById('outputText').innerHTML = text;
}

// 处理表单提交
function submitForm() {
    const text = document.getElementById('inputText').value;
    const dataset = document.getElementById('dataset').value;
    const model = document.getElementById('model').value;
    console.log('Submitting text: "' + text + '", dataset: "' + dataset + '", model: "' + model + '"');
    fetch('/predict_by_text', {
        method: 'POST',
        body: new URLSearchParams({
            'text': text,
            'dataset': dataset,
            'model': model
        }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
        .then(response => response.json())
        // .then(data => highlightEntities(data))
        .then(data => {
            const entities = data.entities;
            const outputText = document.getElementById('outputText');
            outputText.innerHTML = '';
            outputText.textContent = text;
            highlightEntities(entities);
        }).catch(error => console.error("error: ", error));
}