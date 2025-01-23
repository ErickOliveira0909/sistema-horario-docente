async function CadastrarProfessor() {
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const dados = { nome: nome, email: email, senha: senha };

    try {
        const response = await fetch('/cadastrar_professor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        // Verificar se a resposta foi bem-sucedida
        if (response.ok) {
            const result = await response.json();
            window.location.href = result.redirect_url
            
        } else {
            alert('Erro ao cadastrar professor.');
        }
    } catch (error) {
        console.error('Erro de rede ou outro erro:', error);
        alert('Erro ao tentar cadastrar professor.');
    }
}
async function CadastrarDisciplina() {
    const nome = document.getElementById('nome').value;
    const dados = { nome: nome};

    try {
        const response = await fetch('/cadastrando_disciplina', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        // Verificar se a resposta foi bem-sucedida
        if (response.ok) {
            const result = await response.json();
            if(result.redirect_url){
                //window.location.href = result.redirect_url
            }
            else{
                alert(result.message)
            }
            
        } else {
            alert('Erro ao cadastrar professor.');
        }
    } catch (error) {
        console.error('Erro de rede ou outro erro:', error);
        alert('Erro ao tentar cadastrar professor.');
    }
}
async function Login() {
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const dados = {email: email, senha: senha };

    try {
        const response = await fetch('/verificar_login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        // Verificar se a resposta foi bem-sucedida
        if (response.ok) {
            const result = await response.json();
            if(result.redirect_url){
                window.location.href = result.redirect_url
            }
            else{
                alert(result.message)
            }
            
        } else {
            alert('Erro na requisição');
        }
    } catch (error) {
        console.error('Erro de rede ou outro erro:', error);
        alert('Erro de rede ou outro erro.');
    }
}
