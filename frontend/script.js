const API_URL = "http://localhost:8000/api/chamados/";

async function listarChamados() {
    const lista = document.getElementById("lista-chamados");
    lista.innerHTML = "<p>Carregando...</p>";

    try {
        const resposta = await fetch(API_URL);
        const chamados = await resposta.json();

        if (chamados.length === 0) {
            lista.innerHTML = "<p>Nenhum chamado cadastrado.</p>";
            return;
        }

        lista.innerHTML = chamados.map((chamado) => `
          <article>
            <strong>#${chamado.id} — ${chamado.titulo || "Sem título"}</strong>
            <p>${chamado.descricao || "Sem descrição"}</p>
            <p>Status: ${chamado.status}</p>
          </article>
        `).join("");
    } catch (erro) {
        lista.innerHTML = "<p class='erro'>Não foi possível consultar a API.</p>";
    }
}

document.getElementById("form-chamado").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const mensagem = document.getElementById("mensagem");
    const dados = {
        titulo: document.getElementById("titulo").value,
        descricao: document.getElementById("descricao").value,
        status: document.getElementById("status").value
    };

    try {
        const resposta = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        if (!resposta.ok) {
            mensagem.className = "erro";
            mensagem.textContent = "Erro ao cadastrar chamado.";
            return;
        }

        mensagem.className = "sucesso";
        mensagem.textContent = "Chamado cadastrado com sucesso.";
        document.getElementById("form-chamado").reset();
        listarChamados();
    } catch (erro) {
        mensagem.className = "erro";
        mensagem.textContent = "A API não está disponível.";
    }
});

document.getElementById("atualizar").addEventListener("click", listarChamados);

listarChamados();
