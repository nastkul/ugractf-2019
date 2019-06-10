#include <stdio.h>
#include <unistd.h>
#include <curses.h>
#include <wchar.h>
#include <locale.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int W = 80;
int H = 24;

char PRESS_SPACE[] = "НАЖМИТЕ ПРОБЕЛ ЧТОБЫ НАСТРОИТЬ СВОЙ АРБАЛЕТ";
char TITLE_1[] = "У вас есть волшебная стрела и магический арбалет.";
char TITLE_2[] = "Попадите в Сибирь, чтобы получить флаг!";

char* bow_anim[] =
{
    "-||===|>",
    "/||===|>",
    "/|| ==|=>",
    "/||  =|==>",
    "/||   |===>",
    "/||   |",
    "/||   |    ",
};

char* vektor[] =
{
    "wwwwwwwww",
    "|  O  O |",
    "|  /..\\ |",
    "|   ~~  |",
    " \\uuuuu/",
    "    |",
    "    /___(-||===|>",
    "    /_____/",
    "    |",
    "    |",
    "   / \\",
    "  /   \\",
    " /     \\ "
};

// graphics

bool key_pressed(void)
{
    int ch = getch();
    return ch == ' ';
}

void cmvprintw(int y, char* text)
{
    int x = (W - strlen(text) / 2) / 2;
    mvprintw(y, x, "%s", text);
}

void binput(int* value, char* label, const int dy)
{
    bool idle = true;
    int cpos = 0;
    int cval = 0;

    cbreak();
    noecho();
    nodelay(stdscr, TRUE);

    while (idle)
    {
        for (cpos = 0; cpos < 80; cpos++)
        {
            char cstr[] = "                                         ";
            cval = cpos < 40 ? cpos : 80 - cpos;
            cstr[cval] = cpos < 40 ? '>' : '<';
            cmvprintw(dy, label);

            mvprintw(dy + 1, 18, "%s", "┌─────────────────────────────────────────┐");
            mvprintw(dy + 2, 18, "│%s│", cstr, cval);
            mvprintw(dy + 3, 18, "%s", "└─────────────────────────────────────────┘");

            if (key_pressed())
            {
                idle = false;
                break;
            }

            refresh();
            usleep(0x1ABAB);
        }
        *value = cval;
    };
}

void draw_logo(void)
{
    bool idle = true;; 
    unsigned char logo_parts[] =
    {
        0x3c, 0xf3, 0xcf, 0x0c, 0xe7, 0x23, 0x24, 0x90,
        0x48, 0xa4, 0x11, 0x1f, 0x3c, 0xf3, 0xc9, 0x38,
        0x8e, 0xc9, 0x04, 0x92, 0x49, 0x04, 0x56, 0x48,
        0x3c, 0x92, 0x4e, 0x23, 0xa0, 0xf2, 0x4f, 0x24,
        0xf2, 0x40, 0x04, 0x92, 0x41, 0x24, 0x92, 0x00,
        0x20, 0xb3, 0xcb, 0x3c, 0xb0, 0x01, 0x26, 0x92,
        0x69, 0x06, 0x80, 0x0f, 0x24, 0xf2, 0x48, 0x24,
        0x00
    };
    for (unsigned int i = 0; i < sizeof(logo_parts); i++) {
        unsigned char part = logo_parts[i];
        for (int k = 0; k < 8; k++) {
            int x = (i * 8 + k - 2) % 45 + 18;
            int y = (i * 8 + k - 2) / 45 + 1;
            if (y > 5) {
                y++;
            }
            mvprintw(y, x, "%s", part & (0x80u) ? "█" : " ");
            part <<= 1;
        }
    }
    refresh();
    while (idle)
    {
        cmvprintw(15, TITLE_1);
        cmvprintw(16, TITLE_2);
        cmvprintw(20, PRESS_SPACE);

        if (key_pressed())
        {
            idle = false;
            clear();
            break;
            }
    }
    refresh();
}

void draw_vektor()
{
    clear();
    for (int i = 0; i < 13; i++)
    {
        mvprintw(i + 1, 1, "%s", vektor[i]);
    }
    mvprintw(7, 70, "%s", "С И Б И Р Ь");
    refresh();
}

void update_arrow(int r)
{
    for (int i = 0; i < 66; i++)
    {
        if (i < 6) {
            mvprintw(7, 10, "%s", bow_anim[i]);
        } else if (i < 42) {
            draw_vektor();
            mvprintw(7, 10, "%s", bow_anim[6]);
            mvprintw(7, 12 + i, "%s", "====>");
        } else if (i < 60) {
            draw_vektor();
            mvprintw(7, 10, "%s", bow_anim[6]);
            mvprintw(7 - r * (i - 42), 12 + i, "%s", "====>");
        } else if (r != 0) {
            cmvprintw(7, i % 2 == 0 ? "ТАКИЕ ДЕЛА" : "                    ");
            usleep(300000);
        }
        refresh();
        usleep(20000);
    }
}

// libslw (tm)

bool slw_cmp(double a, double b)
{
    double epsilon = 1e-3;
    for (int i = 0; i < b; i++)
    {
        a--;
    }
    return a > epsilon;
}

bool slw_equ(double a, double b)
{
    return a - b < 1 && a -b > 0;
}

double slw_mlt(double a, double b)
{
    double r = 0;
    for (int i = 0; slw_cmp(b, i); i++)
    {
        for (int k = 0; k < a; k++)
        {
            //r++;
            ++r; // faster
        }
    }
    return r;
}

double slw_pow(double a, int pow)
{
    double r = 1;
    for (int i = 0; i < pow; i++)
    {
        r = slw_mlt(r, a);
    }
    return r;
}

int slw_div(double a, double b)
{
    int r = 0;
    while(slw_cmp(a, 0))
    {
        for (int i = 0; slw_cmp(b, i); i++)
        {
            a--;
        }
        printf("%f\n", a);
        r++;
    }
    return r;
}

double avg(double a, double b)
{
    return (a + b) / 2;
}

int simulate_hit(int ang, int sl, int sr, int leg)
{
    double dt = 1.001;
    double g = 9.8;
    double k = exp(log(0.75) - leg / 10) + 0.25;
    double rad = (ang - 20) * 9 * M_PI / 180;
    double v[2] = {13.37 * (sl / (2 * sr + 1)), 1.337 * (sl / (2 * sr + 1))};
    double a[2] = {0};
    double p[3] = {0};
    double s[2] = {0};
    bool higher = false;

    p[1] = 1.75;

    while (slw_cmp(p[1], 0))
    {
        a[0] = -k * v[0];
        a[1] = -g + -k * v[1];

        v[0] = v[0] + a[0] * dt;
        v[1] = v[1] + a[1] * dt;
        
        s[0] = s[0] + v[0] * dt;
        s[1] = s[1] + v[1] * dt;

        p[0] = s[0] * cos(rad);
        p[1] = s[1]; 
        p[2] = s[2] * sin(rad);

        if (slw_equ(p[0], 1337) && slw_equ(p[1], 64) && slw_equ(p[2], 606))
        {
            clear();
            endwin();
            FILE* fd = fopen("/flag/flag", "r");
            char flag[64];
            fscanf(fd, "%s", flag);
            puts(flag);
            fclose(fd);
            exit(0);
        }

        if (!higher && p[1] > 63) {
            higher = true;
        }
    }

    return higher ? 1 : -1;
}

int main (void)
{
    setlocale(LC_ALL, "");
    initscr();
    curs_set(0);
    cbreak();
    int ang;
    int sgh_l;
    int sgh_r;
    int leg;

    draw_logo();
    binput(&ang, "Угол", 8);
    binput(&sgh_l, "Сила левой руки", 15);
    binput(&sgh_r, "Сила правой руки", 15);
    binput(&leg, "Легендарность", 20);
    draw_vektor();
    update_arrow(simulate_hit(ang, sgh_l, sgh_r, leg));
    clear();
    endwin();

    return 0;
}
