#include <stdio.h>
#include <unistd.h>
#include <curses.h>
#include <wchar.h>
#include <locale.h>
#include <string.h>
#include <math.h>

typedef struct
{
    double x;
    double y;
    double z;
    double vh; 
    double vv; 
    double sh; 
    double sv; 
    double vhp;
    double vvp;
} arrow;

int W = 80;
int H = 24;

char PRESS_SPACE[] = "НАЖМИТЕ ПРОБЕЛ ЧТОБЫ НАСТРОИТЬ СВОЙ АРБАЛЕТ";
char TITLE_1[] = "У вас есть волшебная стрела и магический арбалет.";
char TITLE_2[] = "Попадите в Сибирь, чтобы получить флаг!";

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
            usleep(20000);
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

bool slw_cmp(double a, int b)
{
    double epsilon = 1e-3;
    for (int i = 0; i < b; i++)
    {
        a--;
    }
    return a > epsilon;
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

bool simulate_hit(int ang, int sgh_l, int sgh_r, int leg)
{
    arrow arr; 
    double k;
    double rad;
    double g;
    double dt;

    // every input is [0; 40] int

    arr.vh = (13.370 * sgh_l / (sgh_r + 1)); // initial velocity; ought to be a better way
    arr.vv = (1.337 * sgh_l / (sgh_r + 1));
    arr.y = 1.75;
    ang = (ang - 20) * 9;
    rad = ang * M_PI / 180;
    k = exp(log(0.9) - leg / 10) + 0.1;
    g = 9.8;
    dt = 0.1;

    while (1)
    {
        printf("\n(x %9.3f | y %9.3f | z %9.3f | ↑ %6.2f | → %6.2f", arr.x, arr.y, arr.z, arr.vv, arr.vh);

        arr.vhp = arr.vh;
        arr.vh = arr.vhp - arr.vhp * k;
        arr.sh = arr.sh + avg(arr.vh, arr.vhp);

        arr.vvp = arr.vh;
        arr.vv = arr.vvp - arr.vvp * k * g * dt;
        arr.sv = arr.sv + avg(arr.vv, arr.vvp);

        arr.x = arr.sh * cos(rad);
        arr.y = arr.sv;
        arr.z = arr.sh * sin(rad);
        sleep(1);
    }

    return 1;
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
    binput(&sgh_l, "Сила левой руки", 14);
    binput(&sgh_r, "Сила правой руки", 14);
    binput(&leg, "Легендарность", 20);

    endwin();
    //printf("%d", simulate_hit(ang, sgh_l, sgh_r, leg));
    simulate_hit(40, 40, 0, 20);

    return 0;
}
