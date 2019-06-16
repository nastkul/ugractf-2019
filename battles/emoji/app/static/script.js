document.addEventListener('DOMContentLoaded', () => {
    const emoji = document.getElementById('emoji')
    const text = document.getElementById('text')
    const newEmoji = document.getElementById('new-emoji')
    const newText = document.getElementById('new-text')
    const emojiToText = document.getElementById('emoji-text')
    const textToEmoji = document.getElementById('text-emoji')
    const newTranslation = document.getElementById('new-translation')

    emojiToText.addEventListener('click', () => {
        const init = {
            method: 'POST',
            headers: new Headers({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ type: 'toText', emoji: emoji.value })
        }
        fetch('/translate', init).then((r) => r.text()).then((r) => {
            text.value = r
        })
    })

    textToEmoji.addEventListener('click', () => {
        const init = {
            method: 'POST',
            headers: new Headers({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ type: 'toEmoji', text: text.value })
        }
        fetch('/translate', init).then((r) => r.text()).then((r) => {
            emoji.value = r
        })
    })

    newTranslation.addEventListener('click', () => {
        const init = {
            method: 'POST',
            headers: new Headers({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ emoji: newEmoji.value, text: newText.value })
        }
        fetch('/new', init)
    })
})
