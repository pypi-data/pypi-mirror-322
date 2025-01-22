;(() => {
  function centerpointWidget() {
    function movePoint(point, img, x, y) {
      point.style.left = `${img.clientWidth * x}px`
      point.style.top = `${img.clientHeight * y}px`
    }

    for (const field of document.querySelectorAll(
      ".imagefield[data-ppoi-id]",
    )) {
      if (!field.dataset.ppoiId) return
      const ppoiField = document.querySelector(`#${field.dataset.ppoiId}`)
      if (!ppoiField) return

      const point = document.createElement("div")
      const img = field.querySelector("img")
      point.className = "imagefield-point opaque"
      img.parentNode.appendChild(point)

      setTimeout(() => {
        point.className = "imagefield-point"
      }, 1000)

      const matches = ppoiField.value.match(/^([.0-9]+)x([.0-9]+)$/)
      if (matches) {
        movePoint(
          point,
          img,
          Number.parseFloat(matches[1]),
          Number.parseFloat(matches[2]),
        )
      } else {
        movePoint(point, img, 0.5, 0.5)
      }
    }

    document.body.addEventListener("click", (e) => {
      if (e.target?.matches?.("img.imagefield-preview-image")) {
        const field = e.target.closest(".imagefield[data-ppoi-id]")
        if (!field.dataset.ppoiId) return
        const ppoiField = document.querySelector(`#${field.dataset.ppoiId}`)
        if (!ppoiField) return

        const point = field.querySelector(".imagefield-point")
        const img = e.target
        const x = e.offsetX / img.clientWidth
        const y = e.offsetY / img.clientHeight
        ppoiField.value = `${x.toFixed(3)}x${y.toFixed(3)}`
        movePoint(point, img, x, y)
      }
    })
  }

  window.addEventListener("load", centerpointWidget)
})()
