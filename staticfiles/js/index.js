function setFavicon(url) {
            if (document.head) { // Проверяем, существует ли document.head
                const link = document.createElement('link');
                link.rel = 'icon';
                link.href = url;
                document.head.appendChild(link);
            }
        }

// Вызываем функцию с URL изображения после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
          setFavicon('img/zeus_logo.png'); // Важно: используем PNG формат!
      });