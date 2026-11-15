document.addEventListener("DOMContentLoaded", () => {
        const flashAnnouncement = document.getElementById(
        "flash-announcement");
    const successMessages = Array.from(
        document.querySelectorAll(".flash.success"),
        (message) => message.textContent.trim()
    ).filter(Boolean);

    if (flashAnnouncement && successMessages.length > 0) {
        setTimeout(() => {
            flashAnnouncement.textContent = successMessages.join(" ");
        }, 200);
    }    
    
    // Added this for character counter
        document.querySelectorAll("[data-character-counter]").forEach((field) => {
        const counter = document.getElementById(
            field.dataset.characterCounter
        );
        const announcement = document.getElementById(
            `${field.id}-announcement`
        );

        let announcementTimer;

        const getMessage = () => {
            const remaining = field.maxLength - field.value.length;

            if (remaining < 0) {
                const excess = Math.abs(remaining);
                return `${excess} ${
                    excess === 1 ? "character" : "characters"
                } over the limit`;
            }

            return `${remaining} ${
                remaining === 1 ? "character" : "characters"
            } remaining`;
        };

        const updateCounter = () => {
            counter.textContent = getMessage();
        };

        updateCounter();

        field.addEventListener("input", () => {
            updateCounter();
            clearTimeout(announcementTimer);

            announcementTimer = setTimeout(() => {
                if (document.activeElement === field) {
                    const label = field.labels[0].textContent
                        .replace("*", "")
                        .trim();

                    announcement.textContent =
                        `${label}: ${getMessage()}`;
                }
            }, 600);
        });

        field.addEventListener("blur", () => {
            clearTimeout(announcementTimer);
            announcement.textContent = "";
        });
    });

        const firstInvalid = document.querySelector(
        '.ticket-form [aria-invalid="true"]'
    );

    if (firstInvalid) {
        firstInvalid.focus();
    }
});