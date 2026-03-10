function showView(viewId) {
    document.getElementById('step-welcome').style.display = 'none';
    document.getElementById('step-login').style.display = 'none';
    document.getElementById('step-register').style.display = 'none';
    
    document.getElementById(viewId).style.display = 'block';
}
